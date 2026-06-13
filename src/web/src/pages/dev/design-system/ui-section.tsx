import { LockIcon, MailIcon } from 'lucide-react';
import { useState } from 'react';

import { Button as ShadcnButton } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import {
  Badge,
  Button,
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardMedia,
  CardTitle,
  DividerText,
  IconInput,
  Pagination,
  SearchBar,
  Sidebar,
} from '@/shared/ui';

import { DesignSection, DesignSubSection } from './components';

export function UiSection() {
  const [page, setPage] = useState(2);

  return (
    <>
      <DesignSection
        id="ui-shadcn"
        title="UI Components · shadcn 基础"
        description="src/web/src/components/ui/"
      >
        <div className="space-y-8">
          <DesignSubSection title="Button">
            <div className="flex flex-wrap items-center gap-3">
              <ShadcnButton>Default CTA</ShadcnButton>
              <ShadcnButton variant="outline">Outline</ShadcnButton>
              <ShadcnButton variant="ghost">Ghost</ShadcnButton>
              <ShadcnButton variant="destructive">Destructive</ShadcnButton>
              <ShadcnButton disabled>Disabled</ShadcnButton>
              <ShadcnButton size="sm">Small</ShadcnButton>
            </div>
          </DesignSubSection>

          <DesignSubSection title="Input / Label">
            <div className="grid max-w-md gap-4">
              <Input placeholder="默认输入框" />
              <Input placeholder="禁用状态" disabled />
              <Input placeholder="错误状态" aria-invalid="true" defaultValue="invalid@example" />
              <div className="flex items-center gap-2">
                <Checkbox id="ds-label-demo" defaultChecked />
                <Label htmlFor="ds-label-demo">Label 示例</Label>
              </div>
            </div>
          </DesignSubSection>

          <DesignSubSection title="Checkbox">
            <div className="flex flex-wrap items-center gap-6">
              <div className="flex items-center gap-2">
                <Checkbox id="cb-default" />
                <Label htmlFor="cb-default">未选中</Label>
              </div>
              <div className="flex items-center gap-2">
                <Checkbox id="cb-checked" defaultChecked />
                <Label htmlFor="cb-checked">已选中（品牌金）</Label>
              </div>
              <div className="flex items-center gap-2">
                <Checkbox id="cb-disabled" disabled />
                <Label htmlFor="cb-disabled">禁用</Label>
              </div>
            </div>
          </DesignSubSection>

          <DesignSubSection title="Separator">
            <Separator />
          </DesignSubSection>
        </div>
      </DesignSection>

      <DesignSection
        id="ui-composite"
        title="UI Components · 复合组件"
        description="src/web/src/shared/ui/"
      >
        <div className="space-y-8">
          <DesignSubSection title="Button（STONEX variants）">
            <div className="flex flex-wrap items-center gap-3">
              <Button>Default</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="inquiry">Inquiry</Button>
              <Button variant="ghost">Ghost</Button>
              <Button size="cta">CTA</Button>
              <Button size="catalog">Catalog 44px</Button>
              <Button size="pagination">3</Button>
            </div>
          </DesignSubSection>

          <DesignSubSection title="Badge">
            <div className="flex flex-wrap gap-2">
              <Badge variant="inStock">现货</Badge>
              <Badge variant="new">新品</Badge>
              <Badge variant="hotSale">热销</Badge>
              <Badge variant="neutral">默认</Badge>
            </div>
          </DesignSubSection>

          <DesignSubSection title="Card">
            <Card className="max-w-sm">
              <CardMedia aspect="product" className="rounded-t-card">
                <div className="flex h-full items-center justify-center text-[11px] text-muted">
                  130px 图片区
                </div>
              </CardMedia>
              <CardHeader className="p-0 px-3.5 pt-3">
                <CardTitle>产品卡标题 13px</CardTitle>
                <CardDescription>规格说明 11px / leading 1.5</CardDescription>
              </CardHeader>
              <CardFooter className="border-0 px-3.5 pb-3.5 pt-3">
                <span className="text-[15px] font-medium text-primary">
                  ¥ 128<span className="text-[10px] text-muted">/m²</span>
                </span>
              </CardFooter>
            </Card>
          </DesignSubSection>

          <DesignSubSection title="SearchBar">
            <SearchBar onSearch={() => undefined} onAiFindBrick={() => undefined} />
          </DesignSubSection>

          <DesignSubSection title="Sidebar">
            <div className="overflow-hidden rounded-card border border-border-default">
              <Sidebar
                sections={[
                  {
                    id: 'texture',
                    title: '纹理',
                    items: [
                      { id: 'marble', label: '大理石', checked: true },
                      { id: 'granite', label: '花岗岩' },
                    ],
                  },
                ]}
              />
            </div>
          </DesignSubSection>

          <DesignSubSection title="Pagination">
            <Pagination page={page} totalPages={8} onPageChange={setPage} />
          </DesignSubSection>

          <DesignSubSection title="IconInput / DividerText">
            <div className="grid max-w-md gap-6">
              <IconInput icon={MailIcon} placeholder="带图标输入框" />
              <IconInput icon={LockIcon} placeholder="错误示例" error="密码格式不正确" />
              <DividerText>其他登录方式</DividerText>
            </div>
          </DesignSubSection>
        </div>
      </DesignSection>
    </>
  );
}
